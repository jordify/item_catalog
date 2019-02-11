#Item Catalog
##Overview
##Quick Start Guide
##Background
####Problem Statement
Develop an application that lists items of various categories and has a user 
authentication system leverging OAuth and Flask.

The homepage should list all Categories currently in the system along with the latest added items e.g. Stick (Hockey). Selecting a category should show all items in that category and selecting an item
should show specific information about that item. 

Authenticated users should have the ability to add, update, or delete items. 

The application should also provide a JSON endpoint which, at the least, describes all items in the catalog.
####Rubric items
1. API Endpoints
   - Criteria: Does the project implement a JSON endpoint with all required content?
   - Spec: Implements a JSON endpoint that serves the same information as displayed in the HTML endpoints for an arbitrary item in the catalog
2. CRUD: Read
   - Does the website read category and item info from the database?
3. CRUD: Create
   - Does the website include a form allowing users to add new items and correctly processes the forms?
4. CRUD: Update
   - Website include a form to update/edit a record in the database?
5. CRUD: Delete
   - Website indludes a function to delete a record?
6. Authentication & Authorization
   - Create, delete, and update operations do consider authorization status prior to execution
   - Page implements a third-party authentication & authorization service
   - Login and Logout buttons are in the project
7. Code Quality
   - Code is ready for personal review, neatly formatted, and PEP 8 compliant
8. Comments
   - Comments are present and effectively explain longer code procedures
9. Documentation
   - `README` file includes details of all the steps required to successfully run the application

##To Do
- [ ] Database build
- [ ] Flask Build
- [ ] CSS Dev
- [ ] HTML build
- [ ] API Dev
- [ ] User Auth
- [ ] User Auth Alternative Service
- [ ] Write README Quick Start Guide
- [ ] Comment Code
