from django.shortcuts import render
from .models import Blogs
from django.core.files.storage import FileSystemStorage
from collections import OrderedDict
from django.shortcuts import redirect
from django.utils import timezone
import hashlib
from problem2.settings import BASE_DIR

#method defining encryption of file(as file is not to be decrypted so i use hashlib)
def encrypt_it(rootdir, filename, blocksize=2**20):
    m = hashlib.md5()
    with open( rootdir+ filename , "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update( buf )
    return m.hexdigest()

#method of homepage
def index(request):
   blogs=Blogs.objects.order_by('-createdTime')
   d=OrderedDict()
   for i in blogs:
           content=i.fileblog_updated_content.split('\n')
           chr_content=i.charblog
           # fp.close()
           d[i.id]=[content,'fileblog',chr_content]
   return render(request,'blogging/index.html',{'blogs':d})

#This method is invoked whenever new fileblog is to be created
def onFilePress(request):
    return render(request, 'blogging/fileinput.html')

#This method do all the proceesing after file has been uploaded succesfully
def after_fileInput(request):
    if request.method=='POST':
                file1=request.FILES['filed']
                fs = FileSystemStorage()
                filename = fs.save(file1.name, file1)
                file_url=fs.url(filename)
                fp = open(BASE_DIR + str(file_url), 'r',encoding='utf8')
                content=fp.read()
                fp.close()
                # form=Blogs(fileblog=file_url,fileblog_content=content,fileblog_updated_content=content)
                # form.save()
                enc_char = encrypt_it(BASE_DIR, str(file_url))
                print(enc_char)
                form=Blogs(fileblog=file_url,charblog=enc_char,charblog_updated_content=enc_char,fileblog_content=content,fileblog_updated_content=content)
                form.save()
                return redirect('/blogging')

#This method is invoked for updatation of file
def after_updt(request):
    id=request.GET.get('blg_updt')
    print(id)
    data=Blogs.objects.filter(id=id)
    content = data[0].fileblog_updated_content
    return render(request,'blogging/updt_file.html',{'blog':content,'id':id})

#This method do all the processing for updating file blog
def after_fileInput_updt(request):
    id=request.POST.get('id')
    data=Blogs.objects.filter(id=id)
    old_content=data[0].fileblog_updated_content
    new_content=request.POST.get('files')
    n=new_content.split('\n')
    old_chr=data[0].charblog_updated_content

    if old_content!=new_content:
        fp = open(BASE_DIR + str(data[0].fileblog), 'w',encoding='utf8')
        fp.writelines(n)
        fp.close()
        file_url=data[0].fileblog
        enc_char = encrypt_it(BASE_DIR, str(file_url))
        Blogs.objects.filter(id=id).update(fileblog_content=old_content,charblog=enc_char,charblog_upated_content=old_chr,fileblog_updated_content=new_content,updationTime=timezone.now())

    return redirect('/blogging')

#This method shows updated blogs
def show_updt(request):
    data=Blogs.objects.order_by("-updationTime")
    print(data)
    d = OrderedDict()
    for i in data:
            content = i.fileblog_content
            updt_content=i.fileblog_updated_content
            chr_content=i.charblog
            chr_updt_content=i.charblog_updated_content
            if i.updationTime==i.createdTime:
                action_is='creation'
            else:
                action_is='updation'
            d[i.id] = [content, 'File Blog',updt_content,action_is,chr_content,chr_updt_content]
    return render(request,'blogging/updated_contents.html',{'blogs':d})