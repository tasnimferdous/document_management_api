# Personal document management api using Django Rest Framework

## This project helps you upload a document of your own choice, update, delete and share with other users.

* The core app includes the models.py where I've created one single model class named "Document"
* The class has all the information about the document like title, description, document format or extension type, the main file/document, creation time and update time etc.
* The class has a foreign key field "owner" related to the user who created the document and a many to many field named "shared_users" related to the same table user since I wanted to separate the owner and shareholers separately.
* To view, create, update or delete you need to be an authenticated user.
* Default or built-in authentication genetes a token while logging in. You have to use that token to be authenticated.
* If you are a staff/admin you can access all the documents and modify them.
* Otherwise You can only view the documents you created and shared with.
* You can view other's documents that you are shared with but you can't edit them.
* You can only edit or delete the documents that you own.
* It has some amaizing valodation like if you select format of file/document as "pdf" you have to upload pdf type file, you can't upload a file more than 5mb etc.
* Finally you can see the swagger documentation.


## The endpoints are -

-> [POST]       api/sign-up/<br>
-> [POST]       api/sign-in/<br>
-> [GET]        api/document/<br>
-> [POST]       api/document/<br>
-> [GET]        api/document//<int:pk/>/<br>
-> [PUT]        api/document/<int:pk>/<br>
-> [DELETE]     api/document/<int:pk>/<br>
-> [Swagger]    api/schema/swagger-ui/<br>


## To run this project locally -

1. First clone the repository
1. Install the requirements.txt file
2. Modify the settings.py and urls.py files accordingly