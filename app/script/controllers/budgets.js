(function() {

var piper = angular.module('piper');

piper.controller('BudgetListCtrl', ['$scope', 'Restangular',
  function TransactionListCtrl($scope, Restangular) {
    $scope.budgets = Restangular.all('budget').getList();
  }
]);

piper.controller('BudgetAuditCtrl', ['$scope', 'Restangular',
  function TransactionListCtrl($scope, Restangular) {
    $scope.transactions = Restangular.all('budget/audit').getList();
  }
]);

})();