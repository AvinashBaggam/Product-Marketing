1	Dr. Kelli Melton	peggy45@miller-hoffman.com	brand world-class niches
2	Kimberly Noble	shane09@gmail.com	drive efficient e-services
3	Katie Williams	robertvega@yahoo.com	matrix integrated vortals
4	Peggy Welch	aaronmurphy@dean.info	streamline back-end initiatives
5	Kathy Rojas	raymond39@wood-vazquez.biz	redefine granular communities
6	Michael Campbell	reesezachary@gmail.com	utilize integrated infrastructures
7	Melanie Bailey	wanda71@hotmail.com	transition robust e-business
8	Zachary Howard	rlambert@hotmail.com	transition visionary initiatives
9	John Smith	ewade@hotmail.com	engage efficient interfaces
10	Colin Valdez	donaldhernandez@yahoo.com	revolutionize user-centric functionalities
11	Demo	user@gmail.com	abc

CREATE TABLE categories2(
	DOC_ID text,
	LABEL  text,
	RATING number,
	VERIFIED_PURCHASE text,
	PRODUCT_CATEGORY text,
	PRODUCT_ID integer NOT NULL,
	PRODUCT_TITLE text,
	REVIEW_TITLE text	
	REVIEW_TEXT text
);

COPY categories1 (DOC_ID, LABEL, RATING, VERIFIED_PURCHASE, PRODUCT_CATEGORY, PRODUCT_ID, PRODUCT_TITLE, REVIEW_TITLE, REVIEW_TEXT) FROM stdin;

COPY categories1 (DOC_ID, LABEL, RATING, VERIFIED_PURCHASE, PRODUCT_CATEGORY, PRODUCT_ID, PRODUCT_TITLE, REVIEW_TITLE, REVIEW_TEXT) FROM 'C:\Users\abaggam\Desktop\product_genius.sql'
	
CREATE TABLE categories (
    cat_id integer NOT NULL,
    cat_name text
);


CREATE TABLE products (
    asin text NOT NULL,
    title text NOT NULL,
    description text,
    price double precision NOT NULL,
    image text NOT NULL,
    scores json,
    n_scores integer,
    pg_score double precision,
    pos_words json,
    neg_words json
);