class StackTests(c: Stack) extends Tester(c) {
    var nxtDataOut = 0
    val stack = new ScalaStack[Int]()

    for (t <- 0 until 16) {
        val enable = rnd.nextInt(2)
        val push = rnd.nextInt(2)
        val pop = rnd.nextInt(2)
        val dataIn = rnd.nextInt(256)
        val dataOut = nxtDataOut

        if (enable == 1) {
            if (stack.length > 0)
                nxtDataOut = stack.top

            if (push == 1 && stack.length < c.depth) {
                stack.push(dataIn)
            } else if (pop == 1 && stack.length > 0) {
                stack.pop()
            }
        }

        poke(c.io.pop, pop)
        poke(c.io.push, push)
        poke(c.io.en, enable)
        poke(c.io.dataIn, dataIn)

        step(1)
        
        expect(c.io.dataOut, dataOut)
    }
}