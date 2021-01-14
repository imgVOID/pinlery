# PINLERY 
#### CMS for an automatic Pinterest-based website creation.
### Simple Pinterest parsing with the Python [API](https://github.com/imgVOID/pinlery/blob/new/pinlery/init_api.py) - now you can use Pinterest as a free modern managed imagebase!
[![Open Source Helpers](https://www.codetriage.com/imgvoid/pinlery/badges/users.svg)](https://www.codetriage.com/imgvoid/pinlery)
[![Gitter](https://badges.gitter.im/pinlery/community.svg)](https://gitter.im/pinlery/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
### FEATURES
* Fast Pinterest to Django model object convertor. Synchronise your website media with a Pinterest board, section or profile - it's a fully automatic and easy customisable process.
* Ready-to-use Django gallery website app. Also, Pinlery is using some well-documented modern Front End technologies like the [IntersectionObserver lazy load](https://github.com/imgVOID/pinlery/blob/new/gallery/static/gallery/js/lazy_loader.js) and an already configured Bootstrap 4, Isotope, Fancybox, Mmenu plugins.
* Stylish fancy trendy  neumorphism templates and theme for FREE!

### INSTALLATION
1. `git clone https://github.com/imgVOID/pinlery.git`
2. Activate your virtual environment
2. `pip install -r requirements.txt`
3. Configure your database in settings.py
3. `python manage.py migrate`
4. `python manage.py createsuperuser`
5. `python manage.py makemigrations gallery`
7. `python manage.py migrate`
8. `python manage.py runserver`
9. All done! Now visit your `localhost:8000/gallery/`!


### TECHNOLOGIES LIST
* BACK-END (PYTHON):
1. django 3
2. requests
3. fontawesome-free
* FRONT-END (JS, CSS):
1. Bootstrap 4
2. Isotope 3
3. Fancybox 3
4. Mmenu.JS
5. FontAwesome 5
6. Themesberg Neumorphism


### TODO LIST
* Add whitenoise support.
* Add custom JQuery scrollbar.
* Remove hardcoded datasource.
* Add page transition animations.
* Add tabs and links to the Mmenu.
* Add a delete function to the synchronisation.
* Add the jumbotron styling on the showcase page.
* Add animation duration to the grid items on the page load event.
* (Future) Create the Redis-based caching.
* (Future) Admin panel customisation (maybe Grapelli).
* (Future) Isotope, Packery, Masonry, Macy.JS integration.
###### DONE
* ~~Add "scroll to top" button.~~
* ~~Integrate a lazy image load.~~
* ~~Add the size field for a pin model.~~
* ~~Add detailed pagination to the top.~~
* ~~Add fullscreen-default Fancybox mode.~~
* ~~Integrate Isotope to the Bootstrap 4 grid.~~
* ~~Migrate from the Isotope to the Macy.JS~~
* ~~Migrate from the Macy.JS to the Isotope.~~
* ~~Add fixed left and right pagination arrows.~~
* ~~Change Mmenu.JS test data to a dynamic data.~~
* ~~Add the sorting position value number for a pins.~~
* ~~(Option) Add pagination arrows to the top showcase's jumbotron.~~
* ~~(BUG) Add an auto filling for the slug field on a board object creation event.~~
