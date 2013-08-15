(function() {

var piper = angular.module('piper');

piper.controller('TransactionListCtrl', ['$scope', '$http', 'Restangular',
  function TransactionListCtrl($scope, $http, Restangular) {
    var localId = 1000;
    $scope.searched = false;
    $scope.searchResults = [];
    $scope.transactions = [];
    $scope.orderProp = ['justAdded', '-purchase_date','-id'];

    Restangular.all('transaction').getList().then(function(transactions) {
      $scope.transactions = transactions;
    });

    $scope.addNew = function() {
      var trans = {
        purchase_date: +moment().startOf('day'),
        splits: [],
        editing: true,
        justAdded: true,
        localId: localId++
      };
      $scope.transactions.unshift(trans);
    };

    $scope.$watch('query', function(key, oldVal, newVal) {
      search();
      return newVal;
    });

    function search() {
      if ($scope.query) {
        $http.post('/api/search', $scope.query)
          .success(function(data) {
            $scope.searchResults = data;
            $scope.searched = true;
          })
          .error(function() {
            $scope.searchResults = [];
            $scope.searched = true;
          });
      } else {
        $scope.searched = false;
      }
    }

    $scope.transVisible = function(trans) {
      if (!$scope.searched) {
        return true;
      }
      if (trans.justAdded) {
        return true;
      }
      var index = _.pluck($scope.searchResults, 'id').indexOf(trans.id);
      return index >= 0;
    }
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
      $scope.trans.justAdded = undefined;
      $scope.trans.localId = undefined;

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
        var i;
        for (i = 0; i < $scope.transactions.length; i++) {
          var other = $scope.transactions[i];
          var matches = ($scope.trans.id === other.id) ||
            ($scope.trans.localId === other.localId && other.localId !== undefined);
          if (matches) {
            $scope.transactions.splice(i, 1);
            break;
          }
        }
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
