from django.db import models

class ImageManager(models.Manager):

  def get_weighted_random_object(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, filename, score, votecount
            FROM %s
            ORDER BY RANDOM ()
            LIMIT 1
        """ % self.model._meta.db_table)
        res = cursor.fetchone()
        cursor.close()
        if not res:
          return None
        i = self.model(id=res[0], filename=res[1],
                        score=res[2], votecount=res[3])
        return i

class Image(models.Model):
  filename = models.CharField(max_length=10)
  score = models.IntegerField()
  votecount = models.IntegerField()
  session = models.CharField(max_length=40) # Same size as the column in the session table

  objects = ImageManager()

  def __unicode__(self):
      return "%s : %d/%d" % (self.filename, self.score, self.votecount)
