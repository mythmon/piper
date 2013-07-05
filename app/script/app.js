angular.module('piper', ['piperServices'])
  .config(['$routeProvider', '$locationProvider',
    function($routeProvider, $locationProvider) {

      $locationProvider.html5Mode(true);

      $routeProvider
        .when('/transactions', {
          templateUrl: '/static/partials/transaction-list.html',
          controller: TransactionListCtrl
        })
        .when('/transaction/:id', {
          templateUrl: '/static/partials/transaction-detail.html',
          controller: TransactionDetailCtrl
        })

        .otherwise({redirectTo: '/transactions'});
    }
  ]);
