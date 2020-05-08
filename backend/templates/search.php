<!DOCTYPE html>
<html lang="en">
<head>
    <title>Search Results</title>
    <meta charset="utf-8">
    <meta name="format-detection" content="telephone=no"/>
    <link rel="icon" href="images/favicon.ico" type="image/x-icon">
    <link rel="stylesheet" href="css/grid.css">
    <link rel="stylesheet" href="css/mailform.css"/>
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="css/search.css"/>

    <script src="js/jquery.js"></script>
    <script src="js/jquery-migrate-1.2.1.js"></script>

    <!--[if lt IE 9]>
    <html class="lt-ie9">
    <div style=' clear: both; text-align:center; position: relative;'>
        <a href="http://windows.microsoft.com/en-US/internet-explorer/..">
            <img src="images/ie8-panel/warning_bar_0000_us.jpg" border="0" height="42" width="820"
                 alt="You are using an outdated browser. For a faster, safer browsing experience, upgrade for free today."/>
        </a>
    </div>
    <script src="js/html5shiv.js"></script>    
  	<script src='js/selectivizr-min.js'></script>
    <![endif]-->

    <script src='js/device.min.js'></script>
</head>

<body>
<div class="page">
   <!--========================================================
                            HEADER
  =========================================================-->
  <header>
   <section class="panel">
      <div class="container">
          <ul class="inline-list">
              <li><a href="#">Forums</a></li>
              <li><a href="#">Community </a></li>
              <li><a href="#">Affiliates </a></li>
              <li><a href="#">Help</a></li>
          </ul>
          <div class="btn-wr-header">
              <a href="#" class="btn2">Create an account</a>
              <a href="#" class="btn2">Sign In</a>
          </div>
      </div>
    </section>
    <div id="stuck_container" class="stuck_container">
      <div class="container">
        <div class="brand">
          <h1 class="brand_name">
            <a href="./">scripts</a>
          </h1>
          <p class="brand_slogan">
            Online Scripts Directory 
          </p>
        </div>

        <nav class="nav">
          <ul class="sf-menu" data-type="navbar">
            <li>
              <a href="./">Home</a>
            </li>
            <li>
              <a href="index-1.html">About</a>
            </li>
            <li>
              <a href="index-2.html">Most Viewed </a>
            </li>
            <li>
              <a href="index-3.html">Highest rated</a>
              <ul>
                <li>
                  <a href="#">Lorem ipsum dolor </a>
                </li>
                <li>
                  <a href="#">Ait amet conse</a>
                </li>
                <li>
                  <a href="#">Ctetur adipisicing elit</a>
                  <ul>
                    <li>
                      <a href="#">Latest</a>
                    </li>
                    <li>
                      <a href="#">Archive</a>
                    </li>
                  </ul>
                </li>
                <li>
                  <a href="#">Sed do eiusmod </a>
                </li>
                <li>
                  <a href="#">Tempor incididunt </a>
                </li>
              </ul>
            </li>
            <li class="active">
              <a href="index-4.html">Contact Us</a>
            </li>
          </ul>
        </nav>
      </div>
    </div>

  </header>
  <!--========================================================
                            CONTENT
  =========================================================-->
  <main>
    <section class="bg-img well-top">
      <div class="container">
        <div class="row">
          <div class="col-xs-12 col-sm-offset-2 col-sm-8">
            <form class="search-form" action="search.php" method="GET" accept-charset="utf-8">
              <label class="search-form_label">
                <input class="search-form_input" type="text" name="s" autocomplete="off" placeholder="Search Scripts"/>
                <span class="search-form_liveout"></span>
              </label>
              <button class="search-form_submit fa-search" type="submit"></button>
            </form>          
          </div>
        </div>
      </div>        
    </section>
    <section id="content" class="content well5">
        <div class="container ">
            <h4>Search Results</h4>
            <div id="search-results"></div>
        </div>
    </section>
  </main>

  <!--========================================================
                            FOOTER
  =========================================================-->
  <footer>
    <div class="container">
      <div class="brand">
        <h1 class="brand_name">
          <a href="./">scripts</a>
        </h1>
        <p class="brand_slogan">
          Online Scripts Directory 
        </p>
      </div>
    </div>
    <hr/>
    <div class="container well6">
      <div class="row">
        <div class="col-md-2 col-sm-6 col-xs-6">
          <h4>About</h4>
          <ul class="list">
              <li><a href="#">Lorem ipsum</a></li>
              <li><a href="#">Dolor sit amet</a></li>
              <li><a href="#">Conse ctetur adipisicing</a></li>
              <li><a href="#">Elit sed do eiusmod</a></li>
              <li><a href="#">Tempor</a></li>
              <li><a href="#">Incididunt ut labore</a></li>
          </ul>
        </div>
        <div class="col-md-2 col-sm-6 col-xs-16">
          <h4>Need Help?</h4>
          <ul class="list">
              <li><a href="#">Ctetur adipisicing</a></li>
              <li><a href="#">Elit sed do eiusmod</a></li>
              <li><a href="#">Incididunt ut labore</a></li>
              <li><a href="#">Et dolore magna aliqua</a></li>
              <li><a href="#">Ut enim ad mini</a></li>
          </ul>
        </div>
        <div class="col-md-4  col-sm-6 col-xs-6 cl pt">
          <h4>Email Newsletters</h4>
          <form class='mailform subscribe-form' method="post" action="bat/rd-mailform.php"> 
            <input type="hidden" name="form-type" value="contact"/> 
            <fieldset> 
              <label> 
                  <input type="text" 
                  name="email" 
                  placeholder="Enter your E-mail" 
                  data-constraints="@Email @NotEmpty"/> 
              </label> 
              <div class="mfControls"> 
                <button class="fa fa-angle-right" type="submit"></button> 
              </div> 
            </fieldset> 
          </form>             
          <p class="text1">Lorem ipsum dolor sit amet conse ctetur adipisicing elit, sed do eiusmod tempor incididunt ut  labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation.</p>
        </div>
        <div class="col-md-4 col-sm-6 col-xs-6 pt">
          <div class="fb-page" data-href="https://www.facebook.com/TemplateMonster?fref=ts"
             data-width="370" data-height="244" data-hide-cover="false" data-show-facepile="true"
             data-show-posts="false">
            <div class="fb-xfbml-parse-ignore">
                <blockquote cite="https://www.facebook.com/TemplateMonster?fref=ts"><a
                        href="https://www.facebook.com/TemplateMonster?fref=ts">TemplateMonster</a>
                </blockquote>
            </div>
          </div>
        </div>
      </div>
    </div>
    <hr/>
    <div class="container">
      <p class="copy">Scripts © <span id="copyright-year"></span> <a href="https://divorcesus.com">Privacy Policy</a></p>
    </div>
  </footer>
</div>
<div id="fb-root"></div>
<script src="js/script.js"></script>
</body>
</html>
