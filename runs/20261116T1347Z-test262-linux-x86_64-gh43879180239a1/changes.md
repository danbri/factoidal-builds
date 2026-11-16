### Since 20261116T1246Z-test262-linux-x86_64-gh43869545104a1 (core 6e2d790036d4)

Files passed 46,831 -> 46,762 (-69; -0.1283 points)

Newly passing: 0. Newly failing: 69.

Newly failing:

- `test/built-ins/Array/prototype/methods-called-as-functions.js`: FAIL sloppy Test262Error: sort Expected a TypeError to be thrown but no exception was thrown at all
- `test/built-ins/Array/prototype/sort/S15.4.4.11_A3_T1.js`: FAIL sloppy Test262Error: #1: Check ToString operator
- `test/built-ins/Array/prototype/sort/S15.4.4.11_A3_T2.js`: FAIL sloppy Test262Error: #1: Check ToString operator
- `test/built-ins/Array/prototype/sort/S15.4.4.11_A6_T2.js`: FAIL sloppy Test262Error: #5: Object.prototype[1] = -1; Object.prototype.length = 2; Object.prototype.sort = Array.prototype.sort; x = {0:1,1:0}; x.sort(); x[0] === 0. Actu
- `test/built-ins/Array/prototype/sort/call-with-primitive.js`: FAIL sloppy Test262Error: undefined Expected a TypeError to be thrown but no exception was thrown at all
- `test/built-ins/Array/prototype/sort/comparefn-nonfunction-call-throws.js`: FAIL sloppy Test262Error: sample.sort(null); Expected a TypeError to be thrown but no exception was thrown at all
- `test/built-ins/Array/prototype/sort/precise-comparefn-throws.js`: FAIL sloppy Test262Error: Expected SameValue(«undefined», «"get"») to be true
- `test/built-ins/Array/prototype/sort/precise-getter-appends-elements.js`: FAIL sloppy Test262Error: Expected SameValue(«undefined», «"a"») to be true
- `test/built-ins/Array/prototype/sort/precise-getter-deletes-predecessor.js`: FAIL sloppy Test262Error: Expected SameValue(«undefined», «"a"») to be true
- `test/built-ins/Array/prototype/sort/precise-getter-deletes-successor.js`: FAIL sloppy Test262Error: Expected SameValue(«undefined», «"a"») to be true
- `test/built-ins/Array/prototype/sort/precise-getter-increases-length.js`: FAIL sloppy Test262Error: Expected SameValue(«undefined», «"a"») to be true
- `test/built-ins/Array/prototype/sort/precise-getter-pops-elements.js`: FAIL sloppy Test262Error: Expected SameValue(«undefined», «"b"») to be true
- `test/built-ins/Array/prototype/sort/precise-getter-sets-predecessor.js`: FAIL sloppy Test262Error: Expected SameValue(«undefined», «"a"») to be true
- `test/built-ins/Array/prototype/sort/precise-getter-sets-successor.js`: FAIL sloppy Test262Error: Expected SameValue(«undefined», «"a"») to be true
- `test/built-ins/Array/prototype/sort/precise-prototype-accessors.js`: FAIL sloppy Test262Error: Expected SameValue(«undefined», «"get"») to be true
- `test/built-ins/Array/prototype/sort/precise-prototype-element.js`: FAIL sloppy Test262Error: Expected SameValue(«undefined», «4») to be true
- `test/built-ins/Array/prototype/sort/precise-setter-appends-elements.js`: FAIL sloppy Test262Error: Expected SameValue(«undefined», «"a"») to be true
- `test/built-ins/Array/prototype/sort/precise-setter-deletes-predecessor.js`: FAIL sloppy Test262Error: Expected SameValue(«undefined», «"a"») to be true
- `test/built-ins/Array/prototype/sort/precise-setter-deletes-successor.js`: FAIL sloppy Test262Error: Expected SameValue(«undefined», «"a"») to be true
- `test/built-ins/Array/prototype/sort/precise-setter-increases-length.js`: FAIL sloppy Test262Error: Expected SameValue(«undefined», «"a"») to be true
- `test/built-ins/Array/prototype/sort/precise-setter-sets-predecessor.js`: FAIL sloppy Test262Error: Expected SameValue(«undefined», «"a"») to be true
- `test/built-ins/Array/prototype/sort/precise-setter-sets-successor.js`: FAIL sloppy Test262Error: Expected SameValue(«undefined», «"a"») to be true
- `test/built-ins/Array/prototype/splice/S15.4.4.12_A2_T1.js`: FAIL sloppy Test262Error: #2: var obj = {0:0,1:1,2:2,3:3}; obj.length = 4; obj.splice = Array.prototype.splice; var arr = obj.splice(0,3,4,5); arr.length === 3. Actual: 0
- `test/built-ins/Array/prototype/splice/S15.4.4.12_A2_T2.js`: FAIL sloppy Test262Error: #2: var obj = {0:0,1:1}; obj.length = 2; obj.splice = Array.prototype.splice; var arr = obj.splice(-2,-1,2,3); obj.length === 4. Actual: 2
- `test/built-ins/Array/prototype/splice/S15.4.4.12_A2_T3.js`: FAIL sloppy Test262Error: #2: var obj = {0:0,1:1}; obj.length = 2; obj.splice = Array.prototype.splice; var arr = obj.splice(0,-1,2,3); obj.length === 4. Actual: 2
- `test/built-ins/Array/prototype/splice/S15.4.4.12_A2_T4.js`: FAIL sloppy Test262Error: #2: var obj = {0:0,1:1,2:2,3:3}; obj.length = 4; obj.splice = Array.prototype.splice; var arr = obj.splice(-4,3,4,5); arr.length === 3. Actual: 0
- `test/built-ins/Array/prototype/splice/S15.4.4.12_A3_T1.js`: FAIL sloppy Test262Error: #1: var obj = {}; obj.splice = Array.prototype.splice; obj[0] = "x"; obj[4294967295] = "y"; obj.length = 4294967296; var arr = obj.splice(42949672
- `test/built-ins/Array/prototype/splice/S15.4.4.12_A3_T3.js`: FAIL sloppy Test262Error: #3: var obj = {}; obj.splice = Array.prototype.splice; obj[4294967294] = "x"; obj.length = 1; var arr = obj.splice(4294967294,1); obj.length === 0
- `test/built-ins/Array/prototype/splice/S15.4.4.12_A4_T1.js`: FAIL sloppy Test262Error: #7: Object.prototype[1] = -1; Object.prototype.length = 2; Object.prototype.splice = Array.prototype.splice; x = {0:0, 1:1}; var arr = x.splice(1,
- `test/built-ins/Array/prototype/splice/S15.4.4.12_A4_T2.js`: FAIL sloppy Test262Error: #7: Object.prototype[1] = -1; Object.prototype.length = 2; Object.prototype.splice = Array.prototype.splice; x = {0:0, 1:1}; var arr = x.splice(1,
- `test/built-ins/Array/prototype/splice/S15.4.4.12_A4_T3.js`: FAIL sloppy Test262Error: #6: Object.prototype[0] = -1; Object.prototype.length = 1; Object.prototype.splice = Array.prototype.splice; x = {}; var arr = x.splice(0,1); arr.
- `test/built-ins/Array/prototype/splice/S15.4.4.12_A6.1_T3.js`: FAIL sloppy Test262Error: Expected a TypeError
- `test/built-ins/Array/prototype/splice/clamps-length-to-integer-limit.js`: FAIL sloppy Test262Error: Length is 2**53 Expected SameValue(«9007199254740992», «9007199254740991») to be true
- `test/built-ins/Array/prototype/splice/create-non-array-invalid-len.js`: FAIL sloppy Test262Error: Expected a RangeError to be thrown but no exception was thrown at all
- `test/built-ins/Array/prototype/splice/create-proxy.js`: FAIL sloppy Test262Error: Expected SameValue(«», «[object Object]») to be true
- `test/built-ins/Array/prototype/splice/create-revoked-proxy.js`: FAIL sloppy Test262Error: Expected a TypeError to be thrown but no exception was thrown at all
- `test/built-ins/Array/prototype/splice/create-species-undef-invalid-len.js`: FAIL sloppy Test262Error: Expected a RangeError to be thrown but no exception was thrown at all
- `test/built-ins/Array/prototype/splice/length-and-deleteCount-exceeding-integer-limit.js`: FAIL sloppy Test262Error: Actual [] and expected [9007199254740989, 9007199254740990] should have the same contents. The value of result is expected to be ["900719925474098
- `test/built-ins/Array/prototype/splice/length-exceeding-integer-limit-shrink-array.js`: FAIL sloppy Test262Error: Actual [] and expected [9007199254740987] should have the same contents. The value of result is expected to be ["9007199254740987"]
- `test/built-ins/Array/prototype/splice/length-near-integer-limit-grow-array.js`: FAIL sloppy Test262Error: The value of arrayLike.length is expected to be 2 ** 53 - 1 Expected SameValue(«9007199254740990», «9007199254740991») to be true
- `test/built-ins/Array/prototype/splice/set_length_no_args.js`: FAIL sloppy Test262Error: Get('length') called exactly once Expected SameValue(«0», «1») to be true
- `test/built-ins/Array/prototype/splice/throws-if-integer-limit-exceeded.js`: FAIL sloppy Test262Error: Length is 2**53 - 1 Expected a TypeError to be thrown but no exception was thrown at all
- `test/built-ins/JSON/parse/revived-proxy-revoked.js`: FAIL sloppy Test262Error: Expected a TypeError to be thrown but no exception was thrown at all
- `test/built-ins/JSON/parse/revived-proxy.js`: FAIL sloppy Test262Error: proxy for ordinary object Expected SameValue(«false», «true») to be true
- `test/built-ins/JSON/parse/reviver-array-define-prop-err.js`: FAIL sloppy Test262Error: Expected a Test262Error to be thrown but no exception was thrown at all
- `test/built-ins/JSON/parse/reviver-array-delete-err.js`: FAIL sloppy Test262Error: Expected a Test262Error to be thrown but no exception was thrown at all
- `test/built-ins/JSON/parse/reviver-array-get-prop-from-prototype.js`: FAIL sloppy Test262Error: Expected SameValue(«2», «3») to be true
- `test/built-ins/JSON/parse/reviver-array-length-coerce-err.js`: FAIL sloppy Test262Error: Expected a Test262Error to be thrown but no exception was thrown at all
- `test/built-ins/JSON/parse/reviver-array-length-get-err.js`: FAIL sloppy Test262Error: Expected a Test262Error to be thrown but no exception was thrown at all
- `test/built-ins/JSON/parse/reviver-call-args-after-forward-modification.js`: FAIL sloppy Test262Error: Actual [] and expected [key: |0| value: 1 source: |1|, key: |0| value: "barf" source: |undefined|, key: |1| value: ["barf"] source: |undefined|, k
- `test/built-ins/JSON/parse/reviver-call-err.js`: FAIL sloppy Test262Error: Expected a Test262Error to be thrown but no exception was thrown at all
- `test/built-ins/JSON/parse/reviver-call-order.js`: FAIL sloppy Test262Error: Actual [] and expected [1, 2, p1, p2, ] should have the same contents. 
- `test/built-ins/JSON/parse/reviver-forward-modifies-object.js`: FAIL sloppy Test262Error: Expected SameValue(«3», «0») to be true
- `test/built-ins/JSON/parse/reviver-get-name-err.js`: FAIL sloppy Test262Error: Expected a Test262Error to be thrown but no exception was thrown at all
- `test/built-ins/JSON/parse/reviver-object-define-prop-err.js`: FAIL sloppy Test262Error: Expected a Test262Error to be thrown but no exception was thrown at all
- `test/built-ins/JSON/parse/reviver-object-delete-err.js`: FAIL sloppy Test262Error: Expected a Test262Error to be thrown but no exception was thrown at all
- `test/built-ins/JSON/parse/reviver-object-get-prop-from-prototype.js`: FAIL sloppy Test262Error: Expected SameValue(«2», «3») to be true
- `test/built-ins/JSON/parse/reviver-object-own-keys-err.js`: FAIL sloppy Test262Error: Expected a Test262Error to be thrown but no exception was thrown at all
- `test/built-ins/JSON/parse/reviver-wrapper.js`: FAIL sloppy Test262Error: Expected SameValue(«"undefined"», «"object"») to be true
- `test/staging/sm/Array/sort-delete-ascending-order.js`: FAIL sloppy Test262Error: Actual [] and expected [1, 2] should have the same contents. 
- `test/staging/sm/Array/sort_holes.js`: FAIL sloppy Test262Error: Expected [0, 99, -1] to be structurally equal to [-1, 0, 99]. 
- `test/staging/sm/JSON/parse-reviver.js`: FAIL sloppy Test262Error: Expected SameValue(«5», «10») to be true
- `test/staging/sm/extensions/reviver-mutates-holder-array-nonnative.js`: FAIL sloppy Test262Error: Expected SameValue(«1», «null») to be true
- `test/staging/sm/extensions/reviver-mutates-holder-array.js`: FAIL sloppy Test262Error: Expected SameValue(«1», «null») to be true
- `test/staging/sm/extensions/reviver-mutates-holder-object-nonnative.js`: FAIL sloppy Test262Error: Expected SameValue(«0», «null») to be true
- `test/staging/sm/extensions/reviver-mutates-holder-object.js`: FAIL sloppy Test262Error: Expected SameValue(«0», «null») to be true
- `test/staging/sm/misc/builtin-methods-reject-null-undefined-this.js`: FAIL sloppy Test262Error: wrong error for Array.prototype.sort.call(null) Expected a TypeError to be thrown but no exception was thrown at all
- `test/staging/sm/strict/15.4.4.11.js`: FAIL sloppy Test262Error: Expected SameValue(«false», «true») to be true
- `test/staging/sm/strict/15.4.4.12.js`: FAIL sloppy Test262Error: Expected SameValue(«false», «true») to be true

