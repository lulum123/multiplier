import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, Timer


def pack_ui(A: int, B: int) -> int:
    """ui_in[7:4]=A, ui_in[3:0]=B"""
    return ((A & 0xF) << 4) | (B & 0xF)


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start multiplier cocotb test")

    # 1) Start clock (100 kHz: period 10 us)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # 2) Initialize inputs
    dut.ui_in.value = 0
    dut.ena.value = 0
    dut.rst_n.value = 0

    # Hold reset for a few cycles
    await ClockCycles(dut.clk, 5)

    # Release reset
    dut.rst_n.value = 1

    # IMPORTANT:
    # Your RTL pipelines reset: rst_n_2 <= rst_n_1 <= rst_n (2 cycles),
    # so wait >=2 cycles after deasserting rst_n.
    await ClockCycles(dut.clk, 3)

    # 3) Check ena=0 forces A,B=0 -> P=0
    dut.ena.value = 0
    dut.ui_in.value = pack_ui(9, 7)  # doesn't matter when ena=0
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    assert int(dut.uo_out.value) == 0, f"Expected 0 when ena=0, got {int(dut.uo_out.value)}"

    # 4) Random tests with ena=1
    dut.ena.value = 1

    NUM_TESTS = 1000
    for i in range(NUM_TESTS):
        A = random.randint(0, 15)
        B = random.randint(0, 15)

        dut.ui_in.value = pack_ui(A, B)

        # Your RTL registers ui_in_1/ena_1 on posedge,
        # then combinationally assigns A/B from ui_in_1 when ena_1 is 1.
        # So after 1 rising edge, output should reflect new A,B.
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")

        got = int(dut.uo_out.value)
        exp = (A * B) & 0xFF

        assert got == exp, (
            f"Mismatch at test {i}: A={A} B={B}, expected {exp}, got {got}"
        )

    dut._log.info(f"All {NUM_TESTS} tests passed ✅")
