class Comment < ApplicationRecord
  belongs_to :article

  validates :author, presence: true
  validates :body, presence: true, length: { minimum: 5 }

  after_create :update_article_timestamp

  private

  def update_article_timestamp
    article.touch
  end
end
