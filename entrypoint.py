import click
from subprocess import call


@click.command(context_settings={"ignore_unknown_options": True})
@click.argument('service_name')
def run_process(service_name):
    click.echo('Starting service: {}'.format(service_name))
    match service_name:
        case 'tg' | 'telegram' | 'bot' | 'tg_bot' | 'cocker' | 'cocker-tg':
            click.echo('Starting bot...')
            call(['pip', 'list'])
            call(['python', './app.py'])
        case 'audio':
            click.echo('Starting audio...')
            call(['pip', 'list'])
            call(['python', './ms/audio_grpc/app.py'])


if __name__ == "__main__":
    run_process()
