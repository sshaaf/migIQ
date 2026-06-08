# Ruby on Rails Upgrade Example

A minimal Rails 5 application demonstrating upgrade patterns to Rails 7.

## What's Included

- Rails controller with REST actions
- ActiveRecord model with validations
- Database migrations
- Routes configuration
- Gemfile with Rails 5 dependencies

## Migration Challenges

- Rails 5 → Rails 7 API changes
- ActiveRecord query interface updates
- Asset pipeline → Webpacker/Import Maps
- Strong parameters updates
- Zeitwerk autoloader migration
- Deprecation warnings and removals
- Gem compatibility updates

## Demo Migration

```bash
cd examples/rails-upgrade
/migiq "Upgrade this Rails 5 application to Rails 7"
```

**Expected time:** ~3-4 minutes
