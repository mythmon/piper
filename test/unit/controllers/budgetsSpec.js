describe('controllers.budget', function(){
  var $httpBackend, scope;

  beforeEach(module('piper'));

  beforeEach(inject(function(_$httpBackend_, $rootScope) {
    $httpBackend = _$httpBackend_;
    scope = $rootScope.$new();
  }));

  afterEach(function() {
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });

  describe('BudgetListCtrl', function() {
    var ctrl;
    var async = new AsyncSpec(this);

    beforeEach(inject(function($controller) {
      // These are incomplete, because they don't matter.
      $httpBackend.expectGET('/api/budget')
        .respond([ {name: 'Budget 1'}, {name: 'Budget 2'}]);

      ctrl = $controller('BudgetListCtrl', {$scope: scope});
      scope.$apply();
      $httpBackend.flush();
    }));

    async.it('should create "budgets" fetched from xhr', function(done) {
      scope.budgets.then(function(budgets) {
        expect(budgets.length).toBe(2);
        expect(budgets[0].name).toBe('Budget 1');
        expect(budgets[1].name).toBe('Budget 2');
        done();
      });
      scope.$apply();
    });
  });

  describe('BudgetAuditCtrl', function() {
    var ctrl;

    beforeEach(inject(function($rootScope, $controller) {
      $httpBackend.expectGET('/api/budget/audit')
        .respond([{id: 1}, {id: 2}]);

      ctrl = $controller('BudgetAuditCtrl', {$scope: scope});
      scope.$apply();
      $httpBackend.flush();
    }));

    it('should create "transactions" model with 2 transactions fetched from xhr', function() {
      scope.transactions.then(function(transactions) {
        expect(transactions.length).toBe(2);
      });
      scope.$apply();
    });
  });

  describe('BudgetEditCtrl', function() {
    var $routeParams, ctrl;
    var async = new AsyncSpec(this);

    async.it('should request a budget when passed an id', function(done) {
      inject(function($controller) {
        $httpBackend.expectGET('/api/budget/1')
          .respond({'name': 'Budget 1'});

        ctrl = $controller('BudgetEditCtrl', {
          $scope: scope,
          $routeParams: {id: 1}
        });

        scope._budget.then(function(budget) {
          expect(budget.name).toEqual('Budget 1');
          done();
        });

        scope.$apply();
        $httpBackend.flush();
      });
    });

    it('should make a new budget with no id', inject(function($controller) {
      ctrl = $controller('BudgetEditCtrl', {
        $scope: scope,
        $routeParams: {}
      });

      scope._budget.then(function(budget) {
        expect(budget.name).toEqual('Budget 1');
      });
    }));

    async.it('should save a pre-existing budget', function(done) {
      inject(function($controller) {
        $httpBackend.expectGET('/api/budget/1')
          .respond({id: 1});
        ctrl = $controller('BudgetEditCtrl', {
          $scope: scope,
          $routeParams: {id: 1, name: 'Budget 1'}
        });

        scope._budget.then(function(budget) {
          budget.name = 'Budget 1';
          done();
        });

        $httpBackend.expectPUT('/api/budget/1', {id: 1, name: 'Budget 1'})
          .respond({id: 1, name: 'Budget 1'});
        scope.save();
        scope.$apply();
        $httpBackend.flush();
      });
    });

    async.it('should save a not already existing budget', function(done) {
      inject(function($controller, $q) {
        ctrl = $controller('BudgetEditCtrl', {
          $scope: scope,
          $routeParams: {}
        });

        $httpBackend.expectPOST('/api/budget', {name: 'Budget 1'})
          .respond({id: 1});

        scope._budget
          .then(function setName(budget) {
            budget.name = 'Budget 1';
            return budget;
          })
          .then(function waitForSave(budget) {
            var d = $q.defer();
            scope.save().then(function(newBudget) {
              d.resolve(newBudget);
            });
            return d.promise;
          })
          .then(function checkId(budget) {
            expect(budget.id).toEqual(1);
            done();
          });

        scope.$apply();
        $httpBackend.flush();
      });
    });

  });
});