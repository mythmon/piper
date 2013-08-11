(function() {

var piper = angular.module('piper', ['restangular']);

var TMPL_BASE = '/static/partials';

piper.config(['$routeProvider', '$locationProvider',
  function($routeProvider, $locationProvider) {

    $locationProvider.html5Mode(true);

    $routeProvider
      .when('/transaction', {
        templateUrl: TMPL_BASE + '/transaction-list.html',
        controller: 'TransactionListCtrl'
      })

      .when('/budget', {
        templateUrl: TMPL_BASE + '/budget-list.html',
        controller: 'BudgetListCtrl'
      })

      .when('/budget/:id', {
        templateUrl: TMPL_BASE + '/budget-edit.html',
        controller: 'BudgetEditCtrl'
      })

      .when('/audit', {
        templateUrl: TMPL_BASE + '/budget-audit.html',
        controller: 'BudgetAuditCtrl'
      })

      .when('/', {redirectTo: 'transaction'})
      .otherwise({templateUrl: TMPL_BASE + '/404.html'})
  }
]);

piper.config(['RestangularProvider',
  function(RestangularProvider) {
    RestangularProvider.setBaseUrl('/api');
  }
]);

piper.run(function($rootScope, $templateCache) {
  $rootScope.$on('$viewContentLoaded', function() {
    $templateCache.removeAll();
  });
});

})();
