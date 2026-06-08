require_relative 'boot'

require 'rails/all'

Bundler.require(*Rails.groups)

module RailsUpgradeDemo
  class Application < Rails::Application
    config.load_defaults 5.2

    # Classic autoloader (pre-Zeitwerk)
    config.autoloader = :classic

    # Settings in config/environments/* take precedence over those specified here.
    config.time_zone = 'UTC'
    config.active_record.default_timezone = :utc
  end
end
