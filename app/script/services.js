angular.module('piperServices', ['ngResource'])
  .factory('Transaction', function($resource) {
    return $resource('/api/transaction/:id', {id: '@id'});
  });
