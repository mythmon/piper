(function() {

var piper = angular.module('piper');

piper.controller('TransactionListCtrl', ['$scope', 'Transaction',
  function TransactionListCtrl($scope, Transaction) {
    $scope.transactions = Transaction.query();
    $scope.orderProp = 'date';
  }]);


piper.controller('TransactionDetailCtrl', ['$scope', '$routeParams', 'Transaction',
  function($scope, $routeParams, Transaction) {
    $scope.transaction = Transaction.get({id: $routeParams.id});
  }]);


piper.controller('TransactionAddCtrl', ['$scope', '$routeParams', 'Transaction',
  function($scope, $routeParams, Transaction) {
    $scope.trans = {
      splits: [{}]
    };

    $scope.create = function() {
      console.log('Would create', $scope.trans);
    }

    $scope.$watch('trans', function() {
      var i, split;
      var length = $scope.trans.splits.length;
      var fullRows = 0;

      for (i = 0; i < length; i++) {
        split = $scope.trans.splits[i];
        if (!splitIsEmpty(split)) {
          fullRows++;
        }
      }

      if (fullRows === length) {
        $scope.trans.splits.push({});
        length++;
      }

      i = 0;
      console.log('length - fullRows', length - fullRows);
      while (length - fullRows > 1) {
        split = $scope.trans.splits[i];
        if (splitIsEmpty(split)) {
          $scope.trans.splits.splice(i, 1);
          length--;
        } else {
          i++;
        }
      }
    }, true);

    function splitIsEmpty(split) {
      var a = !!split.note;
      var b = !isNaN(split.amount);
      var c = !!split.categories;
      var sum = a || b || c;
      return !sum;
    }
    $scope.splitIsEmpty = splitIsEmpty;
  }]);

})();
