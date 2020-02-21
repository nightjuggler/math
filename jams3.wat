(module
(func (export "inSet")
	(param $zx f64) (param $zy f64)
	(param $cx f64) (param $cy f64) (param $n i32)
	(result i32)
	(local $i i32)   ;; var i = 0
	(local $zx2 f64) ;; var zx2 = 0
	(local $zy2 f64) ;; var zy2 = 0

	(local.set $zx (f64.add (local.get $zx) (local.get $cx))) ;; zx += cx
	(local.set $zy (f64.add (local.get $zy) (local.get $cy))) ;; zy += cy

	(loop $loop
	(local.set $zx2 (f64.mul (local.get $zx) (local.get $zx))) ;; zx2 = zx*zx
	(local.set $zy2 (f64.mul (local.get $zy) (local.get $zy))) ;; zy2 = zy*zy

	;; if (zx2 + zy2 <= 4)
	(if (f64.le (f64.add (local.get $zx2) (local.get $zy2)) (f64.const 4))
		(then

		;; if (++i === n) return -1
		(if (i32.eq (local.tee $i (i32.add (local.get $i) (i32.const 1))) (local.get $n))
			(then (return (i32.const -1))))

		;; zy = cy + 2*zx*zy
		(local.set $zy (f64.add (local.get $cy)
			(f64.mul (f64.mul (f64.const 2) (local.get $zx)) (local.get $zy))))

		;; zx = cx + zx2 - zy2
		(local.set $zx (f64.add (local.get $cx)
			(f64.sub (local.get $zx2) (local.get $zy2))))

		(br $loop)))
	)

	(local.get $i) ;; return i
))
