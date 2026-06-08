class CreateArticles < ActiveRecord::Migration[5.2]
  def change
    create_table :articles do |t|
      t.string :title, null: false
      t.text :body, null: false
      t.string :author, null: false
      t.boolean :published, default: false

      t.timestamps
    end

    add_index :articles, :published
    add_index :articles, :created_at
  end
end
