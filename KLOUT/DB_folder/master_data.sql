
DELETE FROM p_categories;

INSERT INTO p_categories VALUES
	(1,'Computers'),
	(2,'Books'),
	(3,'Foods'),
	(4,'Phones'),
	(5,'Watches');

DELETE FROM products;

INSERT INTO products (id, product_name, description, created_on, want_count, product_image) VALUES
	(1,'DELL','This is a DELL.', '2013-09-03', 0, 'site'),
	(2,'HP','This is a HP.','2013-09-02',1, 'site'),
	(3,'Onepiece','This is a Onepiece.', '2013-09-03', 0, 'site'),
	(4,'Harry Potter','This is a Harry Potter.', '2013-09-03', 0, 'site'),
	(5,'Chinese noodle','This is a Chinese noodle', '2013-09-03', 0, 'site'),
	(6,'Jpanese noodle','This is a Jpanese noodle', '2013-09-03', 0, 'site'),
	(7,'iPhone','This is an iPhene', '2013-09-03', 0, 'site'),
	(8,'GALAXY','This is a GALAXY', '2013-09-03', 0, 'site'),
	(9,'CACIO','This is a CACIO', '2013-09-03', 0, 'site'),
	(10,'G-SHOCK','This is a G-SHOCK', '2013-09-03', 0, 'site');

delete from classification;
insert into classification values (1,1,1),(2,2,1),(3,3,2),(4,4,2),(5,5,3),
(6,6,3),(7,7,4),(8,8,4),(9,9,5),(10,10,5);

select p.* from products p, classification c, p_categories pc where c.product_id = p.id and c.category_id = pc.id and pc.category_name='Watches';