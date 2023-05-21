Installation
Python and Django need to be installed .

pip install django

reqiurements installation


Usage

Customer details have to be available. (preferably in a table and the data entry via REST API)
The customer has the option to enter the products which he/she is willing to sell on that e-commerce site.
Customer should be able to activate or disable the product if necessary.

python manage.py runserver
Then go to the browser and enter the URL http://127.0.0.1:8000/

Do CRUD operation on the products. (adding products to the customer)
Make the product active /inactive. Inactive the product only if it is registered before 2 months.
celery task added for  Inactive the product only if it is registered before 2 months.
