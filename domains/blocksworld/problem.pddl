(define (problem bw-1)
  (:domain blocksworld)

  (:objects A B)

  (:init
    (ontable A)
    (ontable B)
    (clear A)
    (clear B)
    (handempty)
  )

  (:goal
    (on A B)
  )
)