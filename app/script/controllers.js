(function() {

var piper = angular.module('piper');

piper.controller('TransactionListCtrl', ['$scope', 'Restangular',
  function TransactionListCtrl($scope, Restangular) {
    $scope.transactions = Restangular.all('transaction').getList();
    $scope.orderProp = 'date';
  }]);


piper.controller('TransactionDetailCtrl', ['$scope', '$routeParams', 'Restangular',
  function($scope, $routeParams, Restangular) {
    $scope.trans = Restangular.one('transaction', $routeParams.id).get();
  }]);


piper.controller('TransactionAddCtrl', ['$scope', '$routeParams', 'Restangular',
  function($scope, $routeParams, Restangular) {
    $scope.trans = {
      splits: [{}]
    };

    $scope.create = function() {
      var trans = $.extend(true, {}, $scope.trans);
      var i = 0;

      for (i = trans.splits.length - 1; i >= 0; i--) {
        if (splitIsEmpty(trans.splits[i])) {
          trans.splits.splice(i, 1);
          continue;
        }

        trans.splits[i].categories  = trans.splits[i].categories.split(',');
      }

      Restangular.all('transaction').post(trans);
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

      i = length - 1;
      while (length - fullRows > 1) {
        split = $scope.trans.splits[i];
        if (splitIsEmpty(split)) {
          $scope.trans.splits.splice(i, 1);
          length--;
        } else {
          i--;
        }
      }
    }, true);

    function splitIsEmpty(split) {
      return !split.note && !split.amount && !split.categories;
    }
    $scope.splitIsEmpty = splitIsEmpty;
  }]);

})();
