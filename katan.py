from bs4 import BeautifulSoup
import uuid
import  os
import htmlmin
from jsmin import jsmin
import string
import sys, getopt
import argparse



def makeKatan(inputF):
    masterCssFile=os.path.join(outDirCss,os.path.splitext(os.path.basename(inputF))[0]+"_style.css")
    cssFileName=os.path.splitext(os.path.basename(inputF))[0]+"_style.css"
    cssMaster=open(masterCssFile,'w');

    with open(inputF, 'r') as f:
                webpage = f.read().decode('utf-8')
    soup = BeautifulSoup(webpage, "lxml")
    sections = soup.find_all()

    for i in sections:
         try:
             style= i['style']
             css_class_name="_"+str(uuid.uuid4())
             cssMaster.write('.'+css_class_name+'{'+style+'}\n')
             del i['style']
             try:
                 dat= i['class']
                 dat.insert(0,css_class_name)
             except:
                  i['class']=[css_class_name]
                  pass

         except:
             pass

    cssMaster.close();

    for i in  soup.findAll('script'):
        try:
            inline= i['src']
        except:
            data= string.split(str(i), '\n')
            for idx, val in  enumerate(data):
               if "console.log" in val:
                 data[idx]='\n'

            cleanJs='\n'.join(data)
            minified = jsmin(str(cleanJs))
            new_js = BeautifulSoup(minified,'lxml')
            i.replaceWith(new_js.script)

    new_soup = BeautifulSoup('<link rel="stylesheet" href="css/'+cssFileName+'" type="text/css">','html.parser')
    # soup.head.append(new_soup)

    html = soup.prettify("utf-8")

    fname=inputF

    newPath=os.path.join(outDir,os.path.splitext(os.path.basename(fname))[0]+os.path.splitext(os.path.basename(fname))[1]);
    with open(newPath, "wb") as file:
                file.write(str(html))

    with open(newPath, "r") as file:
             code=file.read()

    minified = htmlmin.minify(code.decode("utf-8"), remove_empty_space=True,remove_comments=True)
    new_soup = BeautifulSoup(minified,'html.parser')
    with open(newPath, "w") as file:
         file.write(str(new_soup))








if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='Minify Html website for distribution.')
    parser.add_argument('-i', action="store", dest="in")
    parser.add_argument('-o', action="store", dest="out")

    try:

        outDir=vars(parser.parse_args())['out']
        outDirCss=outDir+'/css'
        inDir=vars(parser.parse_args())['in']

        print "Minimizing:"+inDir
        if not os.path.exists(outDir):
                os.makedirs(outDir)

        if not os.path.exists(outDirCss):
                os.makedirs(outDirCss)


        for file in  os.listdir(inDir):
            try:

                 if os.path.splitext(os.path.basename(file))[1]==".html":
                     print "Processing file:"+os.path.join(inDir,file)
                     makeKatan(os.path.join(inDir,file))
            except:
                print "Skipping -"+os.path.join(inDir,file)
                pass
        print "Done!"
    except:
        print "Error!"
        pass
