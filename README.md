CSS Sorter
==========

This sorts the properties of a CSS-Stream alphabetically to resemble the requirement of the Google Styleguide available at 
http://google-styleguide.googlecode.com/svn/trunk/htmlcssguide.xml#Declaration_Order

##Example

A rule like 
```
.test {
  width: 100px;
  padding: 0;
  -webkit-animation: top 1ms;
}
```
will be sorted as
```
.test {
  -webkit-animation: top 1ms;
  padding: 0;
  width: 100px;
}
```

##Credits

* Written by Thorben Bochenek