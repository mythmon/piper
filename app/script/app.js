(function() {

var piper = angular.module('piper', ['restangular']);

var TMPL_BASE = '/static/partials';

piper.config(['$routeProvider', '$locationProvider',
  function($routeProvider, $locationProvider) {

    $locationProvider.html5Mode(true);

    $routeProvider
      .when('/transactions', {
        templateUrl: TMPL_BASE + '/transaction-list.html',
        controller: 'TransactionListCtrl'
      })

      .when('/budgets', {
        templateUrl: TMPL_BASE + '/budget-list.html',
        controller: 'BudgetListCtrl'
      })

      .when('/budget/add', {
        templateUrl: TMPL_BASE + '/budget-add.html',
        controller: 'BudgetListCtrl'
      })

      .when('/budget/audit', {
        templateUrl: TMPL_BASE + '/budget-audit.html',
        controller: 'BudgetAuditCtrl'
      })

      .otherwise({redirectTo: '/transactions'});
  }
]);

piper.config(['RestangularProvider',
  function(RestangularProvider) {
    RestangularProvider.setBaseUrl('/api');
  }
]);

})();
