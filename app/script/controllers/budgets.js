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

piper.controller('BudgetEditCtrl', ['$scope', '$routeParams', 'Restangular', '$q',
  function($scope, $routeParams, Restangular, $q) {
    if ($routeParams.id && $routeParams.id !== 'add') {
      $scope._budget = Restangular.one('budget', $routeParams.id).get();
    } else {
      $scope._budget = $q.when({});
    }

    $scope._budget.then(function(budget) {
      $scope.budget = budget;
    });

    $scope.save = function() {
      var d = $q.defer();

      $scope._budget.then(function(budget) {
        if (budget.id) {
          d.resolve(budget.put());
        } else {
          return Restangular.all('budget').post(budget)
            .then(function(newBudget) {
              $scope.budget = newBudget;
              d.resolve(newBudget);
            });
        }
      });

      return d.promise;
    }
  }
]);

})();