"""
Role tests
"""
import pytest

# To run all the tests on given docker images:
pytestmark = pytest.mark.docker_images(
    'infopen/ubuntu-trusty-ssh:0.1.0',
)


def test_community_repository_file(SystemInfo, File):
    """
    Test community repository file permissions
    """

    os_distribution = SystemInfo.distribution

    if os_distribution == 'ubuntu':
        repo_file_name = '/etc/apt/sources.list.d/alignak.list'

    repo_file = File(repo_file_name)

    assert repo_file.exists
    assert repo_file.is_file
    assert repo_file.user == 'root'
    assert repo_file.group == 'root'
    assert repo_file.mode == 0o644


def test_ubuntu_community_repository_file_content(SystemInfo, File):
    """
    Test community repository file content on Ubuntu distributions
    """

    if (SystemInfo.distribution != 'ubuntu'):
        pytest.skip('Not apply to %s' % SystemInfo.distribution)

    repo_file = File('/etc/apt/sources.list.d/alignak.list')

    expected_content = (
        'deb http://alignak-monitoring.github.io/repos/deb '
        '{release} main'
    ).format(
        release=SystemInfo.codename
    )

    assert repo_file.contains(expected_content)


def test_packages(Package):
    """
    Test alignak packages are installed
    """

    assert Package('alignak-all').is_installed
