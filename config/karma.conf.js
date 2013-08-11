module.exports = function(config) {
  config.set({
    basePath: '../',
    frameworks: ['jasmine'],
    files: [
      'app/lib/angular.js',
      'app/lib/restangular.js',
      'app/lib/lodash.js',

      'test/lib/jasmine.async.js',
      'test/lib/angular-mocks.js',

      'app/script/**/*.js',

      'test/unit/**/*.js'
    ],
    autoWatch: true,
    browsers: ['PhantomJS']
  });
};
