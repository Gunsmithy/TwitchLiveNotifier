from setuptools import setup

setup(name='twitchlivenotifier',
      version='0.1',
      description='Python script to notify a Discord server when the streamer goes live, with the current game and box art.',
      url='https://github.com/Gunsmithy/TwitchLiveNotifier',
      author='Dylan Kauling',
      author_email='gunsmithy@gmail.com',
      license='GPLv3',
      packages=['twitchlivenotifier'],
	  install_requires=[
          'requests', 'zc.lockfile',
      ],
      entry_points = {
        'console_scripts': ['twitchlivenotifier=twitchlivenotifier.command_line:main'],
      },
      zip_safe=False)
