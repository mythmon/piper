(function() {

var piper = angular.module('piper');

piper.controller('BudgetListCtrl', ['$scope', 'Restangular',
  function TransactionListCtrl($scope, Restangular) {
    var budgets = Restangular.all('budget').getList();

    $scope.budgets = budgets;
  }
]);

})();