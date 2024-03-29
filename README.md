# [uploadcsv.com](http://uploadcsv.com)
### Project Introduction
This is a personal project to create a web app that allows someone to upload different csv files with registration details (eg name, contact details etc) and import into a fixed format database.  

This could be useful for a company that receives lists of customers or members in different csv structures and needs to enter this data into their own database.

Note that the web app is intended as a conceptual project rather than a commercial product. It aims to showcase the programmer's skillset of data management and web dev.

### Functionality  
The web app offers the following functionality:
* upload csv files
* view initial rows (equivalent to df.head() in pandas)
* allows manual matching of columns with predefined field names
* automatically estimates the correct matched fields
* prevents duplicate matches with popup alert - both as selected and when clicking submit
* inserts new column with userID created by web app (option to add prefix to userID)
* view same initial rows for only those columns matched to the predefined field names
* download the data in the new format as a csv file
* demo mode with preloaded csv file
* connects to a DynamoDB database on the backend
* queries the database with a predefined search

### Future Functionality
* tbd

### Structure
* [app.py](https://github.com/howardvickers/uploadcsv/blob/master/src/app.py) is the server.  
* [index.html](https://github.com/howardvickers/uploadcsv/blob/master/src/templates/index.html) is the initial html page (includes upload and demo functions).  
* [upload.html](https://github.com/howardvickers/uploadcsv/blob/master/src/templates/upload.html) is the field matching and download html page (main interface).  

### Technologies Employed
* python
* numpy
* pandas
* flask
* jinja
* javascript
* jquery
* ajax
* bootstrap
* html
* css
* AWS (EC2 & Route 53)
* DynamoDB
* Boto3
