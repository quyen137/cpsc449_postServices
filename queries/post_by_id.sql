-- :name post_by_id :one
SELECT * FROM userdata
WHERE id = :id;