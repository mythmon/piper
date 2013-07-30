(function() {

var piper = angular.module('piper');

piper.controller('TransactionListCtrl', ['$scope', '$http', 'Restangular',
  function TransactionListCtrl($scope, $http, Restangular) {
    var originalTransactions = Restangular.all('transaction').getList();

    $scope.transactions = originalTransactions;
    $scope.orderProp = ['-purchase_date','-id'];

    $scope.addNew = function() {
      $scope.transactions.then(function(transactions) {
        transactions.unshift({
          purchase_date: +moment().startOf('day'),
          splits: [],
          editing: true,
        });
      })
    };

    var searchTimeout = null;
    $scope.watch('query', function(key, oldVal, newVal) {
      if (searchTimeout !== null) {
        clearTimeout(searchTimeout);
      }
      searchTimeout = setTimeout(search, 250);
      return newVal;
    });

    function search() {
      searchTimeout = null;

      if ($scope.query) {
        $http.post('/search', $scope.query).then(function(res) {
          $scope.transactions = res.data;
        });
      } else {
        $scope.transactions = originalTransactions;
      }
    }
  }
]);


piper.controller('TransactionDetailCtrl', ['$scope', '$routeParams', 'Restangular',
  function($scope, $routeParams, Restangular) {
    $scope.trans = Restangular.one('transaction', $routeParams.id).get();
  }
]);


piper.controller('TransactionRow', ['$scope', 'Restangular',
  function($scope, Restangular) {
    $scope.editing = !!$scope.trans.editing;
    delete $scope.trans.editing;
    $scope.$watch('trans.splits', update, true);
    update();

    $scope.edit = function() {
      $scope.editing = !$scope.editing;
      update();

      if (!$scope.editing) {
        $scope.save();
      }
    }

    $scope.save = function() {
      if ($scope.trans.id === undefined) {
        Restangular.all('transaction').post($scope.trans).then(function(resp) {
          $scope.trans = resp;
        });
      } else {
        $scope.trans.put();
      }
    }

    $scope.delete = function() {
      function removeLocal() {
        $scope.transactions.then(function(transactions) {
          var i = transactions.indexOf($scope.trans);
          if (i !== -1) {
            transactions.splice(i, 1);
          }
        });
      }

      if ($scope.trans.id !== undefined) {
        $scope.trans.remove().then(removeLocal)
      } else {
        removeLocal();
      }
    }

    function update() {
      var i;
      var split;
      var length = $scope.trans.splits.length;
      var fullRows = 0;
      var target;

      for (i = 0; i < length; i++) {
        split = $scope.trans.splits[i];
        if (!splitIsEmpty(split)) {
          fullRows++;
        }
      }

      if ($scope.editing) {
        if (fullRows === length) {
          $scope.trans.splits.push({});
          length++;
        }
        target = 1;
      } else {
        target = 0;
      }

      i = length - 1;
      while (length - fullRows > target) {
        split = $scope.trans.splits[i];
        if (splitIsEmpty(split)) {
          $scope.trans.splits.splice(i, 1);
          length--;
        } else {
          i--;
        }
      }
    }

    function splitIsEmpty(split) {
      return !split.note && !split.amount && !split.categories;
    }
 }
]);

})();
