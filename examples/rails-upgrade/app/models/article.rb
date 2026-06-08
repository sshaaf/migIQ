class Article < ApplicationRecord
  has_many :comments, dependent: :destroy

  validates :title, presence: true, length: { minimum: 5, maximum: 200 }
  validates :body, presence: true, length: { minimum: 10 }
  validates :author, presence: true

  scope :published, -> { where(published: true) }
  scope :recent, -> { order(created_at: :desc).limit(10) }

  def published?
    published
  end

  def self.search(query)
    where("title LIKE ? OR body LIKE ?", "%#{query}%", "%#{query}%")
  end
end
