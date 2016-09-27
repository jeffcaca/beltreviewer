def addreview(request):
	if request.POST == "POST":
		reviewvalidate = Review.objects.reviewvalidate(request.POST)
		if reviewvalidate['passed']:
			review = review.objects.justreviewcreate(request.POST, request.session['id'])
			return redirect(reverse('books:index'))
		else:
			for error in reviewvalidate['errors']:
				messages.error(request, error)

			return redirect(reverse('books:viewbook'))

 	url(r"(?P<id>\d+)", views.addreview, name="addreview"),


 		def justreviewcreate(self, data, user_id, id):
		user = User.objects.get(id = user_id)
		book = Book.objects.get(name = id )
		newreview = Review.objects.create(description = data['description'], rating = data['rating'], book=book, user=user)
		print "review printed"

def reviewvalidate(self, data):
		errors = []
		if len(data['description']) < 1:
			errors.append('Please fill out a description')
		reviewresponse = {}
		if errors:
			reviewresponse['passed'] = False
			reviewresponse['errors'] = errors
		else:
			reviewresponse['passed'] = True
		return reviewresponse