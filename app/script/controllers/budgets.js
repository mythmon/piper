(function() {

var piper = angular.module('piper');

piper.controller('BudgetListCtrl', ['$scope', 'Restangular',
  function TransactionListCtrl($scope, Restangular) {
    $scope.budgets = Restangular.all('budget').getList().then(function(budgets) {

      _.each(budgets, function(budget) {
        budget.period = null;

        if (budget.start === null || budget.end === null) {
          return;
        }

        budget.start = new Date(budget.start);
        budget.end = new Date(budget.end);

        var startOnFirsts = budget.start.getDate() === 1 && budget.end.getDate() === 1;
        var subsequentMonths = budget.end.getMonth() - budget.start.getMonth() === 1;
        var subsequentYears = budget.end.getYear() - budget.start.getYear() === 1;
        var yearWrap = budget.start.getMonth() === 11 && budget.end.getMonth() === 0;
        var januaries = budget.start.getMonth() === 0 && budget.end.getMonth() === 0;

        if (startOnFirsts && (subsequentMonths || (yearWrap && subsequentYears))) {
          budget.period = moment(budget.start).format('MMMM');
          return;
        }

        if (startOnFirsts && subsequentYears && januaries) {
          budget.period = budget.start.getFullYear();
          return;
        }

        console.log('something weird happened with dates for ' + budget.name);
        console.log(budget.start.toString(), budget.end.toString());
      });

      return budgets;
    });
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