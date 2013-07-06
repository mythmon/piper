(function() {

var piper = angular.module('piper');

piper.factory('Transaction', ['$resource', function($resource) {
  return $resource('/api/transaction/:id', {id: '@id'});
}]);

})();
