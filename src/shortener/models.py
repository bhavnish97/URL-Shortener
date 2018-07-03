from django.db import models
from django.conf import settings
# Create your models here.
from django.core.urlresolvers import reverse
from django_hosts.resolvers import reverse
from .utils import code_generator,create_shortcode
from .validators import validate_url, validate_dot_com

SHORTCODE_MAX=getattr(settings,"SHORTCODE_MAX",15)

class URLManager(models.Manager):
	def all(self,*args,**kwargs):
		qs_main=super(URLManager,self).all(*args,**kwargs)
		qs=qs_main.filter(active=True)
		return qs


	def refresh_shortcodes(self):
		qs=URL.objects.filter(id__gte=1)
		new_codes=0
		for q in qs:
			q.shortcode=create_shortcode(q)
			print(q.shortcode)
			q.save()
			new_codes+=1
		return "new codes: {i}".format(i=new_codes)	


class URL(models.Model):
	url=models.CharField(max_length=220,validators=[validate_url,validate_dot_com])
	shortcode=models.CharField(max_length=SHORTCODE_MAX,unique=True)
	update=models.DateTimeField(auto_now=True)
	timestamp=models.DateTimeField(auto_now_add=True)
	active=models.BooleanField(default=True)

	objects=URLManager()


	def save(self,*args,**kwargs):
		if self.shortcode is None or self.shortcode=="":
			self.shortcode=create_shortcode(self)

		if not "http" in self.url:
			self.url="http://" + self.url
		super(URL,self).save(*args,**kwargs)
     
	def __str__(self):
		return str(self.url)

	def __unicode__(self):
		return str(self.url)


	def get_short_url(self):
		url_path=reverse("scode",kwargs={'shortcode':self.shortcode},host='www',scheme='http')
		return url_path