from turing.models import Clientes
import csv

def handle_upload_file(f):
	#items = []
	with open(f, 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=";")
	#f.readlines()
		for row in reader:
			obj, created = Clientes.objects.update_or_create(
					name=row[1],
					country=row[2],
					city=row[3],
					category=row[4]
				)
		if created:
			return HttpResponseRedirect(obj.all)
		else:
			return HttpResponse("ya exiiste")
			#items.append(va)
	return obj.all()
