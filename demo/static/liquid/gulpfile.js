/*
|--------------------------------------------------------------------------
| Gulp defintion file
|--------------------------------------------------------------------------
*/
'use strict';

/*
|--------------------------------------------------------------------------
| Gulp includes
|--------------------------------------------------------------------------|
|
*/
var gulp = require('gulp'),
	spritesmith = require('gulp.spritesmith');

//Automatically load any gulp plugins
var $ = require('gulp-load-plugins')();


/*
|--------------------------------------------------------------------------
| Options
|--------------------------------------------------------------------------|
|
*/
var DEV_PATH = '.',
	DIST_PATH = './dist';

var options = {

	// ENVIRONMENT
	ENV             : 'dev',

	// SASS / CSS
	BROWSERS_VERSION : 'last 2 versions',
	SASS_SOURCE     : DEV_PATH + '/scss/**/*.scss',
	SASS_SOURCE_PATH: DEV_PATH + '/scss',
	CSS_PATH        : DEV_PATH + '/css',
	CSS_DIST_PATH   : DIST_PATH + '/css',

	// BOWER - without DEV_PATH
	BOWER_SOURCE    : '/bower_components',

	//JAVASCRIPT
	JS_SOURCE       : DEV_PATH + '/js/**/*.js',
	JS_SOURCE_PATH  : DEV_PATH + '/js',
	JS_DIST_PATH    : DIST_PATH + '/js',

	// Images
	IMAGE_SOURCE    : DEV_PATH + '/images/**/*',
	IMAGE_SOURCE_PATH: DEV_PATH + '/images',
	IMAGE_DIST_PATH      : DIST_PATH + '/images',

	// Fonts
	FONT_SOURCE    : [
					DEV_PATH + '/assets/fonts/**/*'
		],
	FONT_DIST      : DIST_PATH + '/fonts/',
};

/*
|--------------------------------------------------------------------------
| Gulp tasks
|--------------------------------------------------------------------------|
|
*/
// SASS
gulp.task('sass', function() {
	return gulp.src([options.SASS_SOURCE])
		.pipe($.sass({
			outputStyle: 'nested',
			errLogToConsole: true
		}))
		.pipe($.autoprefixer(options.BROWSERS_VERSION))
		.pipe(gulp.dest(options.CSS_PATH));
});


// SCRIPTS
gulp.task('scripts', function () {
	return gulp.src(options.JS_SOURCE)
			.pipe($.jshint('.jshintrc'));
});


//Sprite generator
gulp.task('sprite', function () {
	gulp.start('retina-sprite');
	var spriteData = gulp.src(options.IMAGE_SOURCE_PATH + '/sprite/*.png').pipe(spritesmith({
		cssFormat: 'scss',
		imgName: 'sprite.png',
		cssName: '_sprite.scss',
		imgPath: '../images/sprite.png',
		algorithm: 'binary-tree'
	}));
	spriteData.img.pipe(gulp.dest(options.IMAGE_SOURCE_PATH));
	spriteData.css.pipe(gulp.dest(options.SASS_SOURCE_PATH + '/modules'));
});

//Retina sprite generator
gulp.task('retina-sprite', function () {
  var spriteData = gulp.src(options.IMAGE_SOURCE_PATH + '/retina-sprite/*.png').pipe(spritesmith({
	cssFormat: 'scss',
	imgName: 'retina-sprite.png',
	cssName: '_retina-sprite.scss',
	imgPath: '../images/retina-sprite.png',
	algorithm: 'binary-tree'
  }));
  spriteData.img.pipe(gulp.dest(options.IMAGE_SOURCE_PATH));
  spriteData.css.pipe(gulp.dest(options.SASS_SOURCE_PATH + '/modules'));
});

/*
|--------------------------------------------------------------------------
| Gulp connection and watch tasks
|--------------------------------------------------------------------------|
|
*/
// Connect
gulp.task('connect', $.connect.server({
	root: ['.'],
	port: 9000,
	livereload: true,
	open: {}
}));


// Watch
gulp.task('watch-files', ['connect'], function () {
	gulp.start('sass');

	gulp.watch([
		DEV_PATH + '/*',
		options.CSS_PATH + '/*.css',
		options.JS_SOURCE_PATH + '/**/*.js'
	], function(event) {
		return gulp.src(event.path)
			.pipe($.connect.reload());
	});

	// Watch .scss files
	gulp.watch(options.SASS_SOURCE, ['sass']);
});


gulp.task('dev', function() {
	gulp.start('watch-files');
});

/*
|--------------------------------------------------------------------------
| Gulp default task
|--------------------------------------------------------------------------|
|
*/
gulp.task('watch',['dev']);
