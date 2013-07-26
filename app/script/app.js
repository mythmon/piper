(function() {

var piper = angular.module('piper', ['restangular']);

piper.config(['$routeProvider', '$locationProvider',
  function($routeProvider, $locationProvider) {

    $locationProvider.html5Mode(true);

    $routeProvider
      .when('/transactions', {
        templateUrl: '/static/partials/transaction-list.html',
        controller: 'TransactionListCtrl'
      })

      .when('/transaction/add', {
        templateUrl: '/static/partials/transaction-add.html',
        controller: 'TransactionAddCtrl'
      })

      .when('/transaction/:id', {
        templateUrl: '/static/partials/transaction-detail.html',
        controller: 'TransactionDetailCtrl'
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
