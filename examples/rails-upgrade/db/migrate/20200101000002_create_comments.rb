class CreateComments < ActiveRecord::Migration[5.2]
  def change
    create_table :comments do |t|
      t.references :article, foreign_key: true, null: false
      t.string :author, null: false
      t.text :body, null: false

      t.timestamps
    end

    add_index :comments, :created_at
  end
end
