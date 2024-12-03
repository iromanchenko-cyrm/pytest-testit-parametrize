def test_testit_parametrize_plugin_registered_correctly(pytester):
    """Make sure that pytest accepts our plugin via special entry_point pytest11"""

    # create a temporary pytest test module
    pytester.makepyfile(
        """
        def test_registeration_plugin():
            pass
    """
    )

    # run pytest with the following cmd args
    result = pytester.runpytest(
        "-v",
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "*::test_registeration_plugin PASSED*",
        ]
    )

    assert result.ret == 0


def test_help_message(pytester):
    result = pytester.runpytest(
        "--help",
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "testit-parametrize:",
            "*--testit-params-init*Upload parameters from autotests into Test IT",
        ]
    )
