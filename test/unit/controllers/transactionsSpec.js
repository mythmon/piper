describe('controllers.transaction', function(){
  beforeEach(module('piper'));

  describe('TransactionListCtrl', function() {
    var $httpBackend, scope, ctrl;
    var async = new AsyncSpec(this);

    beforeEach(inject(function(_$httpBackend_, $rootScope, $controller) {
      $httpBackend = _$httpBackend_;
      // These are incomplete, because they don't matter.
      $httpBackend.expectGET('/api/transaction')
        .respond([ {id: 1}, {id: 2}]);

      scope = $rootScope.$new();
      ctrl = $controller('TransactionListCtrl', {$scope: scope});
      scope.$apply();
      $httpBackend.flush();
    }));

    afterEach(function() {
      $httpBackend.verifyNoOutstandingExpectation();
      $httpBackend.verifyNoOutstandingRequest();
    });

    it('should create "transactions" model from xhr', function() {
      expect(scope.transactions.length).toBe(2);
    });

    it('should set orderProp to sort by newly added, date, and id', function() {
      expect(scope.orderProp).toEqual(['justAdded', '-purchase_date', '-id']);
    })
  });

});