import time
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required

from onecalendar.models import CalEntry

mnames = "January February March April May June July August September October November December"
mnames = mnames.split()

@login_required
def index(request, year=None):
	"""Main listing, years and months; three years per page."""
	# prev / next years
	if year: year = int(year)
	else:	 year = time.localtime()[0]

	nowy, nowm = time.localtime()[:2]
	lst = []

	# create a list of months for each year, indicating ones that contain entries and current
	for y in [year, year+1, year+2]:
		mlst = []
		for n, month in enumerate(mnames):
			entry = current = False   # are there entry(s) for this month; current month?
			entries = CalEntry.objects.filter(date__year=y, date__month=n+1)

			if entries:
				entry = True
			if y == nowy and n+1 == nowm:
				current = True
			mlst.append(dict(n=n+1, name=month, entry=entry, current=current))
		lst.append((y, mlst))

	return render_to_response("onecalendar/main.html", dict(years=lst, user=request.user, year=year))
