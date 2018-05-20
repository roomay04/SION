from django.shortcuts import render
from django.db import connection
from django.views.decorators.csrf import csrf_protect

# Create your views here.
def index(request):
    html='fitur3.html'
    return render(request, html) 

response={}
@csrf_protect
def regis_organisasi_post(request):
    if(request.method == 'POST'):
    	response['nama'] = request.POST['nama']
    	response['web'] = request.POST['web']
    	response['email'] = request.POST['email'] 
    	response['kec'] = request.POST['kec'] 
    	response['kab'] = request.POST['kab']
    	response['prov'] = request.POST['prov']
    	response['kodepos'] = request.POST['kodepos']
    	response['jln'] = request.POST['jln']
    	response['tujuan'] = request.POST['tujuan']
    	response['nama_pengurus'] = request.POST['nama_pengurus']
    	response['email_pengurus'] = request.POST['email_pengurus']
    	response['alamat_pengurus'] = request.POST['alamat_pengurus']

    	cur=connection.cursor()
    	cur.execute('SET SEARCH_PATH TO SION')
    	cur.execute('SELECT count(*) FROM ORGANISASI WHERE email_organisasi=%s AND nama=%s',(response['email'], response['nama']))
    	if (cur.fetchone() == 0):
    		cur.execute('INSERT INTO ORGANISASI (email_organisasi,website,nama,provinsi,kabupaten_kota,kecamatan,kelurahan,kode_pos,status_verifikasi) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',(response['email'],response['web'],response['nama'],response['prov'],response['kab'],response['kec'],response['jln'],response['kodepos'],'terverifikasi'))
    		cur.execute('INSERT INTO "USER" (email, password, nama, alamat_lengkap) values (%s, %s, %s, %s)',(response['email_pengurus'], 'abc123', response['nama_pengurus'], response['alamat_pengurus']))
    		cur.execute('INSERT INTO PENGURUS_ORGANISASI (email, organisasi) values (%s,%s)',(response['email_pengurus'],response['nama']))
    		connection.commit()
    		html ='fitur3.5.html'
    		return render(request, html, response)
    	else:
    		html ='fitur3.5 gagal verifikasi.html'
    		return render(request, html, response)
    
    else:        
        return HttpResponseRedirect('/login/')