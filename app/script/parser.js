(function() {

  function searchParser(string) {
    var stream = new Stream(string);
    return parseSearch(stream);
  }

  function parseSearch(stream) {
    return pickRule(stream, [parseBoolean, parseNot, parseAction]);
  }

  function parseAction(stream) {
    var actions = {
      ':': 'contains',
      '!:': 'not-contains',
      '=': 'equals',
      '!=': 'not-equals',
      '>': 'greater',
      '>=': 'greater-equal',
      '<': 'less',
      '<=': 'less-equal'
    };
    var ident = parseIdent(stream);
    // The longest tokens must come first, so don't just iterate the actions keys.
    var action = stream.expect(['!:', '!=', '>=', '<=', ':', '=', '>', '<']);
    var value = parseValueList(stream);

    var match = {};
    match[ident] = value;
    var ret = {};
    ret[actions[action]] = match;
    return ret;
  }

  function parseIdent(stream) {
    var identBodyClass = charClass('a-z', 'A-Z', '0-9', '_');
    var token = stream.expect(charClass('a-z', 'A-Z', '_'));
    var name = '';

    while(token !== null) {
      name += token;
      token = stream.accept(identBodyClass);
    }

    return name;
  }

  function parseValueList(stream) {
    return parseValue(stream);
  }

  function parseValue(stream) {
    var valueClass = charClass('a-z', 'A-Z', '0-9', '-', '_', '.', '/');
    var token = stream.expect(valueClass.concat(['"']));
    var value = '';

    if (token === '"') {
      while (token !== null && token !== '"') {
        token = stream.next();
        if (token === '\\') {
          token = stream.next();
        }
        value += token;
      }
    } else {
      while (token !== null) {
        value += token;
        token = stream.accept(valueClass);
      }
    }

    return value;
  }

  function parseBoolean(stream) {
    var left = pickRule(stream, [parseNot, parseAction], false);
    stream.accept([' ']);
    var op = stream.expect(['AND', 'OR']);
    stream.accept([' ']);
    var right = parseSearch(stream);

    var ret = {};
    ret[op.toLowerCase()] = [left, right];
    return ret;
  }

  function parseNot(stream) {
    stream.expect(['NOT']);
    stream.accept([' ']);
    var target = parseAction(stream);

    return {
      'not': target
    }
  }


  function charClass(/* descs */) {
    var descs = arguments;
    var original = Array.prototype.join.call(descs, ', ');

    var ret = _(descs).map(_class).flatten().valueOf();
    ret.original = function() {
      return original;
    }
    ret.concat = function(other) {
      var n = Array.prototype.concat.call(this, other);
      n.original = this.original;
      n.concat = this.concat;
      return n;
    }
    return ret;

    function _class(desc) {
      var match;
      var i;
      var a, b, step;

      if (desc.length === 1) {
        return [desc];
      }

      match = /(.)-(.)/.exec(desc);
      if (match) {
        a = match[1].charCodeAt(0);
        b = match[2].charCodeAt(0);
        step = a < b ? 1 : -1;
        b += step;

        return _.range(a, b, step).map(function(c) {
          return String.fromCharCode(c);
        });
      }
    }
  }


  /* Iterate through the passed rules, and return the result of the first
   * that succeeds. */
  function pickRule(stream, rules, consume) {
    if (consume === undefined) consume = true;
    var i;
    var ret;
    var originalIndex = stream.index;
    var longestConsumed = 0;
    var error = null;

    for (i = 0; i < rules.length; i++) {
      try {
        var ret = rules[i](stream);
        if (ret !== null && (stream.end() || !consume)) {
          return ret;
        } else {
          throw "Expected end of input, found '" + stream.peek() + "'.";
        }
      } catch (e) {
        if (stream.index > longestConsumed) {
          longestConsumed = stream.index;
          error = e;
        }
        stream.index = originalIndex;
      }
    }

    if (error) {
      throw error;
    } else {
      throw "Syntax error at position " + stream.index + ".";
    }
  }


  function Stream(string) {
    this.index = 0;
    this.stream = string;
  }

  /* Consume the stream until either
   *
   * a) One of the possbiles matches completely, then return it.
   * b) None of the possibles matches. Reset the stream, return null.
   */
  Stream.prototype.accept = function(possibles) {
    var i;

    for (i = 0; i < possibles.length; i++) {
      var a = this.index;
      var b = a + possibles[i].length;
      if (possibles[i] === this.stream.slice(a, b)) {
        this.index = b;
        return possibles[i];
      }
    }

    return null;
  };

  /* Like `accept`, except raise an error instead of returning null. */
  Stream.prototype.expect = function(possibles) {
    var match = this.accept(possibles);

    if (match === null) {
      var expected = possibles;
      var unexpected = this.stream.charAt(this.index) || 'end of string';

      if (expected.original) {
        expected = expected.original();
      }

      throw 'Unexpected ' + unexpected + ' at index ' + this.index + ', ' +
            'expected one of: ' + expected;
    }

    return match;
  }

  /* Return true if the stream is at the end, false otherwise. */
  Stream.prototype.end = function() {
    return this.index === this.stream.length;
  }

  /* Unconsume `n` characters of the stream (default 1) */
  Stream.prototype.back = function(n) {
    if (n === undefined) n = 0;
    this.index -= n;
  }

  /* Consume the next character in the stream and return it, or return
   * null if at the end of the stream. */
  Stream.prototype.next = function() {
    if (this.end()) return null;
    return this.stream.charAt(this.index++);
  }

  /* Return the next character in the stream without consuming it, or
   * return null if at the end of the stream. */
  Stream.prototype.peek = function() {
    if (this.end()) return null;
    return this.stream.charAt(this.index);
  }


  window.searchParser = searchParser;

})();