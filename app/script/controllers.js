TransactionListCtrl.$inject = ['$scope', 'Transaction'];
function TransactionListCtrl($scope, Transaction) {
  $scope.transactions = Transaction.query();
  $scope.orderProp = 'date';

  $scope.setOrderProp = function(orderProp) {
    $scope.orderProp = orderProp;
  }
}


TransactionDetailCtrl.$inject = ['$scope', '$routeParams', 'Transaction'];
function TransactionDetailCtrl($scope, $routeParams, Transaction) {
  $scope.transaction = Transaction.get({id: $routeParams.id});
}
