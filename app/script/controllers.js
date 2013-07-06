(function() {

var piper = angular.module('piper');

piper.controller('TransactionListCtrl', ['$scope', 'Transaction',
  function TransactionListCtrl($scope, Transaction) {
    $scope.transactions = Transaction.query();
    $scope.orderProp = 'date';

    $scope.create = function() {
      var trans = new Transaction($scope.newTrans);
      trans.$save();
      $scope.transactions.push(trans);
    }
  }]);


piper.controller('TransactionDetailCtrl', ['$scope', '$routeParams', 'Transaction',
  function($scope, $routeParams, Transaction) {
    $scope.transaction = Transaction.get({id: $routeParams.id});
  }]);

})();
